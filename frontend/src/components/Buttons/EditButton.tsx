import { PiPencilLineThin } from "react-icons/pi";


const EditButton = ({ onAction }) => {
  return (
    <button
      onClick={onAction}
      className={`p-2 text-gray-300 hover:text-pink-500 transition-colors ease-in duration-300`}
      title="Edit" 
    >
      <PiPencilLineThin size={17}/>
    </button>
  );
};

export default EditButton;