import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Datos from "./components/Datos";
import Ppto from "./components/Ppto";
import Apu from "./components/Apu";
import Gastos from "./components/Gastos";
import Insumos from "./components/Insumos";
import Config from "./components/Config";

function App() {
  const [activeComponent, setActiveComponent] = useState("Main");

  function renderComponent() {
    switch (activeComponent) {
      case "Datos":
        return <Datos />;
      case "Ppto":
        return <Ppto />;
      case "Apu":
        return <Apu />;
      case "Insumos":
        return <Insumos />;
      case "Gastos":
        return <Gastos />;
      case "Config":
        return <Config />;
      default:
        return <></>;
    }
  }

  return (
    <div className="flex h-dvh bg-neutral-50 font-light text-gray-200 dark:bg-neutral-800">
      <Sidebar activeComponent={setActiveComponent} />
      {renderComponent()}
    </div>
  );
}

export default App;
