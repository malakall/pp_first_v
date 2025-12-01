import { useAuth } from "../AuthContext";

export const ProfilePage = () => {
  const { user, loading } = useAuth();

  if (loading) return <div>Загрузка...</div>;
  if (!user) return <div>Вы не авторизованы</div>;

  return (
    <div className="card">
      <h2>Профиль</h2>
      <p><b>ID:</b> {user.id}</p>
      <p><b>Email:</b> {user.email}</p>
    </div>
  );
};
