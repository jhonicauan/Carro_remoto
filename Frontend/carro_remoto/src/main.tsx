import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import Navbar from './Components/Navbar.tsx'
createRoot(document.getElementById('root')!).render(
  <>
    <Navbar />
    <App />
  </>
)
