import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import TicketsPage from './pages/TicketsPage';
import CreateTicketPage from './pages/CreateTicketPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<CreateTicketPage />} />
          <Route path="tickets" element={<TicketsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;