import { IoAddCircleOutline } from "react-icons/io5";

const AddButton = ({ onAction, size }) => {
  return (
    <button
      onClick={onAction}
      className=" text-gray-400 transition-colors ease-in duration-300 hover:text-pink-500">
      <IoAddCircleOutline size={size} />
    </button>
  );
};

export default AddButton;
