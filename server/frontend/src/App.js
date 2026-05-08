import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register"; // 1. Додаємо імпорт компонента реєстрації
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      {/* 2. Додаємо маршрут для реєстрації */}
      <Route path="/register" element={<Register />} /> 
    </Routes>
  );
}
export default App;
