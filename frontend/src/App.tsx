import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { HelmetProvider } from 'react-helmet-async';
import theme from './theme';
import Layout from './components/Layout/Layout';
import Home from './pages/Home';
import CourseDetail from './pages/CourseDetail';
import Courses from './pages/Courses';
import Profile from './pages/Profile';
import './styles/global.css';

// Создаем клиент React Query
const queryClient = new QueryClient();

function App() {
  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Router>
            <Box sx={{ width: '100vw', overflowX: 'hidden' }}>
              <Layout>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/courses" element={<Courses />} />
                  <Route path="/courses/:id" element={<CourseDetail />} />
                  <Route path="/profile" element={<Profile />} />
                </Routes>
              </Layout>
            </Box>
          </Router>
        </ThemeProvider>
      </QueryClientProvider>
    </HelmetProvider>
  );
}

export default App;
