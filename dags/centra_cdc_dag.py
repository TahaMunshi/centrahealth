from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaConsumer
import json
import psycopg2
import logging

LOG = logging.getLogger("airflow.task")

def ingest_topic(topic):
    # track offsets between DAG runs
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',    # on first-ever start only
        enable_auto_commit=True,         # tell Kafka to commit after poll()
        group_id='centra_cdc_group',     # fixed group id
        consumer_timeout_ms=5000,        # exit if no new messages for 5s
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    conn = psycopg2.connect(
        host='postgres', port='5432',
        dbname='centrahealth', user='centrauser', password='centrapass'
    )
    cur = conn.cursor()

    msg_count = 0
    for msg in consumer:
        msg_count += 1
        payload = msg.value.get('payload') or {}
        op = payload.get("op")
        after = payload.get("after") or {}

        if topic.endswith(".patient") and after and op in ("c", "u", "r"):
            cur.execute(
                """
                INSERT INTO central_patient (cnic, full_name, dob, gender, phone)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (cnic) DO UPDATE SET
                  full_name   = EXCLUDED.full_name,
                  dob         = EXCLUDED.dob,
                  gender      = EXCLUDED.gender,
                  phone       = EXCLUDED.phone;
                """,
                (
                    after["cnic"],
                    after["full_name"],
                    after["dob"],
                    after["gender"],
                    after["phone"],
                ),
            )

        if topic.endswith(".record") and after and op in ("c", "u", "r"):
            doc_email = after["doctor_email"]
            cur.execute(
                """
                INSERT INTO doctor (email, full_name, hospital_src)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
                """,
                (doc_email, after.get("doctor_name", ""), topic.split(".")[0]),
            )
            cur.execute("SELECT doctor_id FROM doctor WHERE email = %s", (doc_email,))
            doctor_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO hospital_record (patient_cnic, doctor_id, visit_date, notes)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    after["patient_cnic"],
                    doctor_id,
                    after["visit_date"],
                    after["notes"],
                ),
            )

    # commit DB changes _once_ after the loop
    conn.commit()
    LOG.info(f"Processed {msg_count} messages from {topic}")

    cur.close()
    conn.close()
    consumer.close()


def make_task(topic):
    return PythonOperator(
        task_id=f'ingest_{topic.replace(".", "_")}',
        python_callable=ingest_topic,
        op_kwargs={'topic': topic},
    )


with DAG(
    'centra_cdc_to_central',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2025, 4, 17),
        'retries': 0,
        'retry_delay': timedelta(minutes=1),
    },
    schedule_interval='*/5 * * * *',
    catchup=False,
) as dag:

    topics = [
        'ziauddin.public.patient',
        'ziauddin.public.record',
        'agakhan.public.patient',
        'agakhan.public.record',
    ]

    tasks = [make_task(t) for t in topics]

    # this just ensures all four run in parallel
    for t in tasks:
        t
