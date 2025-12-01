import { Link } from "react-router-dom";
import { useAuth } from "../AuthContext";

export const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <span className="logo">HeatMap ML</span>
        {user && (
          <>
            <Link to="/profile">Профиль</Link>
            <Link to="/upload">Загрузить видео</Link>
            <Link to="/history">Мои тепловые карты</Link>
          </>
        )}
      </div>
      <div className="navbar-right">
        {!user ? (
          <>
            <Link to="/login">Вход</Link>
            <Link to="/register">Регистрация</Link>
          </>
        ) : (
          <button onClick={logout}>Выйти</button>
        )}
      </div>
    </nav>
  );
};
