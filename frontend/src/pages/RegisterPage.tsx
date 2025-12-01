import type { FormEvent } from "react";
import { useState } from "react";
import { useAuth } from "../AuthContext";
import { useNavigate } from "react-router-dom";

export const RegisterPage = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await register(email, password);
      navigate("/profile");
    } catch (err: any) {
      setError(err.message || "Ошибка регистрации");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Регистрация</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input
            value={email}
            onChange={e => setEmail(e.target.value)}
            type="email"
            required
          />
        </label>
        <label>
          Пароль
          <input
            value={password}
            onChange={e => setPassword(e.target.value)}
            type="password"
            required
          />
        </label>
        {error && <div className="error">{error}</div>}
        <button disabled={loading}>
          {loading ? "Создаём..." : "Зарегистрироваться"}
        </button>
      </form>
    </div>
  );
};
