import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Intelligence from './pages/Intelligence';
import Discovery from './pages/Discovery';
import Orchestration from './pages/Orchestration';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Intelligence />} />
          <Route path="discovery" element={<Discovery />} />
          <Route path="orchestration" element={<Orchestration />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
