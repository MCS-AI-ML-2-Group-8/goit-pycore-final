import { GoCheckCircle } from "react-icons/go";
import { RxCrossCircled } from "react-icons/rx";

const EditableInput = ({
  value,
  onChange,
  onSave,
  onCancel,
  className = "",
  type = "input",
}) => {
  return (
    <div
      className={`flex items-center gap-3 transition-all ease-in duration-500 ${className}`}>
      {type === "textarea" ? (
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="bg-gray-600 text-indigo-100 px-2 py-1 rounded-md outline-none focus:border-fuchsia-500 resize-none"
          rows={2}
        />
      ) : (
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="bg-gray-600 text-indigo-100 px-2 py-1 rounded-lg max-w-45 outline-none focus:border-fuchsia-500"
        />
      )}
      <div className="flex gap-2">
        <button
          onClick={onSave}
          className="text-green-500 hover:text-green-400 hover:scale-110 transition-all duration-200">
          <GoCheckCircle size={20} />
        </button>
        <button
          onClick={onCancel}
          className="text-red-500 hover:text-red-400 hover:scale-110 transition-all duration-200">
          <RxCrossCircled size={20} />
        </button>
      </div>
    </div>
  );
};

export default EditableInput;
