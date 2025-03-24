import { registerAllModules } from "handsontable/registry";
import { HotTable } from "@handsontable/react-wrapper";
import { atom, useAtom } from "jotai";

registerAllModules();

const hotAtom = atom<any[][]>([
  ["1", "Obras Provisionales", "glb", 1, 2, 2],
  ["2", "Arquitectura", "m²", 1, 2, 2],
  ["3", "Estructuras", "m³", 1, 2, 2],
  ["4", "Instalaciones Sanitarias", "m", 1, 2, 2],
  ["5", "Instalaciones Eléctricas", "m", 1, 2, 2],
]);

function Ppto() {
  const [tableData, setTableData] = useAtom(hotAtom);

  return (
    <div className="flex grow flex-col overflow-clip">
      <span className="p-4 text-3xl">Presupuesto</span>
      <div className="ht-theme-main-dark-auto flex-grow overflow-y-auto p-0">
        <HotTable
          afterChange={(changes, source) => {
            if (changes && source !== "loadData") {
              setTableData([...tableData]);
            }
          }}
          data={tableData}
          columns={[
            { col: "Item", className: "htLeft" },
            { index: "Descripción", className: "htLeft", type: "text" },
            { index: "Und", className: "htCenter", type: "text" },
            {
              index: "Metrado",
              className: "htRight",
              type: "numeric",
              allowInvalid: false,
              numericFormat: {
                pattern: "0,0.00",
              },
            },
            {
              index: "Precio",
              className: "htRight",
              type: "numeric",
              allowInvalid: false,
              readOnly: true,
              numericFormat: {
                pattern: "0,0.00",
              },
            },
            {
              index: "Parcial",
              className: "htRight",
              type: "numeric",
              allowInvalid: false,
              readOnly: true,
              numericFormat: {
                pattern: "0,0.00",
              },
            },
          ]}
          rowHeaders={false}
          colHeaders={["Item", "Descripción", "Und", "Metrado", "Precio", "Parcial"]}
          autoWrapRow={true}
          autoWrapCol={true}
          licenseKey="non-commercial-and-evaluation"
          minSpareRows={1}
          stretchH="all"
          width="100%"
          height="auto"
          contextMenu={{
            items: {
              copy: {},
              cut: {},
              "---------": {},
              row_above: {},
              row_below: {},
              remove_row: {},
            },
          }}
          hiddenColumns={{
            columns: [],
            indicators: true,
            copyPasteEnabled: false,
          }}
          manualColumnMove={false}
          manualColumnFreeze={true}
          manualColumnResize={true}
          filters={false}
          hiddenRows={{
            rows: [],
            indicators: true,
            copyPasteEnabled: false,
          }}
          manualRowMove={true}
          manualRowResize={true}
          columnSorting={true}
          mergeCells={true}
        />
      </div>
    </div>
  );
}

export default Ppto;
