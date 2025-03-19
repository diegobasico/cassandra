import Sidebar from "./components/Sidebar";
import Main from "./components/Main";

function App() {
  return (
    <div className="flex h-dvh bg-neutral-50 text-gray-200 dark:bg-neutral-800">
      <Sidebar />
      <Main />
    </div>
  );
}

export default App;
