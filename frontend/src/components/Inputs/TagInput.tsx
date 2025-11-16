import { GoCheckCircle } from "react-icons/go";
import { RxCrossCircled } from "react-icons/rx";

const TagInput = ({
  value,
  onChange,
  onSave,
  onCancel,
}) => {
  return (
    <div
      className={`flex items-center gap-3 w-1`}>
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="bg-gray-600 text-indigo-100 px-2 py-1 rounded-3xl w-22 outline-none border border-transparent text-xs focus:border-fuchsia-500"
        />
      <div className="flex gap-2">
        <button
          onClick={onSave}
          className="text-green-500 hover:text-green-400 hover:scale-110 transition-all duration-200 focus:outline-none">
          <GoCheckCircle size={20} />
        </button>
        <button
          onClick={onCancel}
          className="text-red-500 hover:text-red-400 hover:scale-110 transition-all duration-200 focus:outline-none">
          <RxCrossCircled size={20} />
        </button>
      </div>
    </div>
  );
};

export default TagInput;
