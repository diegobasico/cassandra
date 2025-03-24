import { useEffect, useState } from "react";

function Gastos() {
  const [width, setWidth] = useState(window.innerWidth);

  const handleResize = () => {
    setWidth(window.innerWidth);
  };

  useEffect(() => {
    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div className="flex flex-col p-4">
      <span className="text-3xl">Gastos</span>
      <span>{width}</span>
    </div>
  );
}

export default Gastos;
