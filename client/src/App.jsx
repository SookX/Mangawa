import { BrowserRouter, Routes, Route } from "react-router-dom"
import DataProvider from "./context/DataContext"
import LayoutGrid from "./components/LayoutGrid/LayoutGrid"
import Login from "./pages/Login/Login"
import Register from "./pages/Register/Register"

function App() {

  return (
    <BrowserRouter>

      <DataProvider>

        <LayoutGrid type='screen' />

        <Routes>

            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

        </Routes>

      </DataProvider>

    </BrowserRouter>
  )
}

export default App
