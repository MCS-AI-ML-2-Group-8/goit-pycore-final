import { useState } from "react";
import { addContactTag, deleteContactTag } from "../../api/api";
import { RxCross1 } from "react-icons/rx";
import { IoAddCircleOutline } from "react-icons/io5";
import TagInput from "../Inputs/TagInput";
import AddButton from "../Buttons/AddButton";

const TagSection = ({ contactId, tags, onUpdate }) => {
  const [addingTag, setAddingTag] = useState(false);
  const [newTag, setNewTag] = useState("");

  const handleAddTag = () => {
    setAddingTag(true);
  };

  const handleSaveNewTag = async () => {
    try {
      await addContactTag(contactId, newTag);
      onUpdate((prev) => ({
        ...prev,
        tags: [...prev.tags, newTag],
      }));
      setAddingTag(false);
      setNewTag("");
    } catch (error) {
      console.error("Error adding tag:", error);
    }
  };

  const handleCancelNewTag = () => {
    setAddingTag(false);
    setNewTag("");
  };

  const handleDeleteTag = async (tag: string) => {
    try {
      await deleteContactTag(contactId, tag);
      onUpdate((prev) => ({
        ...prev,
        tags: prev.tags.filter((t) => t !== tag),
      }));
    } catch (error) {
      console.error("Error deleting tag:", error);
    }
  };

  return (
    <div className="contact-section">
      <div className="flex justify-between items-center"></div>
      <div className="contact-tags">
        {tags.map((tag, i) => (
          <span key={i} className="tag inline-flex items-center gap-1">
            {tag}
            <button
              onClick={() => handleDeleteTag(tag)}
              className="text-indigo-100 transition-colors ease-in duration-300 hover:text-red-500 text-xs">
              <RxCross1 size={10} />
            </button>
          </span>
        ))}
        {addingTag ? (
          <TagInput
            value={newTag}
            onChange={setNewTag}
            onSave={handleSaveNewTag}
            onCancel={handleCancelNewTag}
          />
        ) : (
          <AddButton onAction={handleAddTag} />
        )}
      </div>
    </div>
  );
};

export default TagSection;
