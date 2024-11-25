import { BrowserRouter, Routes, Route } from "react-router-dom"
import DataProvider from "./context/DataContext"
import LayoutGrid from "./components/LayoutGrid/LayoutGrid"
import Login from "./pages/Login/Login"
import Register from "./pages/Register/Register"
import Dashboard from "./pages/Dashboard/Dashboard"
import Activate from "./pages/Activate/Activate"

function App() {

  return (
    <BrowserRouter>

      <DataProvider>

        <LayoutGrid type='screen' />

        <Routes>

            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/activate/:uidb64/:token" element={<Activate />} />

            <Route path="/dashboard" element={<Dashboard />} />

        </Routes>

      </DataProvider>

    </BrowserRouter>
  )
}

export default App
