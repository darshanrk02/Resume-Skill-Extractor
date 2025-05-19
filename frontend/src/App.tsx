import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './styles/theme';
import { NotificationProvider } from './context/NotificationContext';

// Layout
import Layout from './components/layout/Layout';

// Pages
import SummaryPage from './pages/SummaryPage';
import JDMatchingPage from './pages/JDMatchingPage';
import ResumeSearchPage from './pages/ResumeSearchPage';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NotificationProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<SummaryPage />} />
              <Route path="/jd-matching" element={<JDMatchingPage />} />
              <Route path="/resumes" element={<ResumeSearchPage />} />
            </Routes>
          </Layout>
        </Router>
      </NotificationProvider>
    </ThemeProvider>
  );
}

export default App;
