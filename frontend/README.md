# Hospital Dashboard

A modern, responsive hospital dashboard built with React, Material-UI, and TypeScript. This application provides different views for administrators, doctors, and patients.

## Features

- Role-based authentication (Admin, Doctor, Patient)
- Responsive design that works on desktop and mobile
- Modern Material-UI components
- TypeScript for type safety
- Protected routes
- Real-time data updates

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hospital-dashboard
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Development

To start the development server:

```bash
npm start
```

The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build:

```bash
npm run build
```

The build files will be created in the `build` directory.

## Docker Deployment

To build and run the Docker container:

```bash
docker build -t hospital-dashboard .
docker run -p 80:80 hospital-dashboard
```

## Project Structure

```
src/
  ├── components/     # Reusable UI components
  ├── contexts/       # React contexts (auth, theme, etc.)
  ├── layouts/        # Layout components
  ├── pages/          # Page components
  ├── services/       # API services
  ├── types/          # TypeScript type definitions
  └── utils/          # Utility functions
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
