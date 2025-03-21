import { atom, useAtom } from "jotai";

const formAtom = atom({
  name: "",
  age: "",
});

function Datos() {
  const [formState, setFormState] = useAtom(formAtom);

  return (
    <div className="p-4">
      <span className="text-3xl"> Datos Generales</span>
      <input
        type="text"
        value={formState.name}
        onChange={(event) => setFormState({ ...formState, name: event.target.value })}
        placeholder="Name"
      />
      <input
        type="text"
        value={formState.age}
        onChange={(event) => setFormState({ ...formState, age: event.target.value })}
        placeholder="Age"
      />
    </div>
  );
}

export default Datos;
