
import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState("연결 확인 중...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/health")
      .then((res) => {
        if (!res.ok) throw new Error("API 오류");
        return res.json();
      })
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("백엔드 연결 실패"));
  }, []);

  return (
    <main style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>VIZ</h1>
      <p>Enterprise AI Assistant</p>
      <hr />
      <h2>Backend Status: {status}</h2>
    </main>
  );
}

export default App;
