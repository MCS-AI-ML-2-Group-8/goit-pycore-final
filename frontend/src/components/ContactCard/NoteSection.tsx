// NoteSection.tsx
import { useState } from "react";
import EditButton from "../Buttons/EditButton";
import { addNote, updateNote, addTagToNote } from "../../api/api";
import EditableInput from "../Inputs/EditInput";
import AddButton from "../Buttons/AddButton";
import TagInput from "../Inputs/TagInput";
import type { sign } from "crypto";

interface Note {
  id: number;
  text: string;
  tags: string[];
}

interface NoteSectionProps {
  contactId: number;
  notes: Note[];
  onUpdate: (updater: (prev: any) => any) => void;
}

const NoteSection = ({ contactId, notes, onUpdate }: NoteSectionProps) => {
  const [addingNote, setAddingNote] = useState(false);
  const [newNote, setNewNote] = useState("");
  const [editingNoteId, setEditingNoteId] = useState<number | null>(null);
  const [newNoteText, setNewNoteText] = useState("");
  const [newNoteTags, setNewNoteTags] = useState<string[]>([]);
  const [addingTagToNoteId, setAddingTagToNoteId] = useState<number | null>(
    null
  );
  const [newTagForNote, setNewTagForNote] = useState("");

  const handleAddNote = () => {
    setAddingNote(true);
  };

  const handleSaveNewNote = async () => {
    try {
      const newNoteData = await addNote(contactId, newNote);
      onUpdate((prev) => ({
        ...prev,
        notes: [...prev.notes, newNoteData],
      }));
      setAddingNote(false);
      setNewNote("");
    } catch (error) {
      console.error("Error adding note:", error);
    }
  };

  const handleCancelNewNote = () => {
    setAddingNote(false);
    setNewNote("");
  };

  const handleEditNote = (
    noteId: number,
    currentText: string,
    currentTags: string[]
  ) => {
    setEditingNoteId(noteId);
    setNewNoteText(currentText);
    setNewNoteTags(currentTags);
  };

  const handleSaveNote = async () => {
    if (editingNoteId === null) return;
    try {
      await updateNote(editingNoteId, newNoteText);
      onUpdate((prev) => ({
        ...prev,
        notes: prev.notes.map((note: Note) =>
          note.id === editingNoteId
            ? { ...note, text: newNoteText, tags: newNoteTags }
            : note
        ),
      }));
      setEditingNoteId(null);
      setNewNoteText("");
      setNewNoteTags([]);
    } catch (error) {
      console.error("Error updating note:", error);
    }
  };

  const handleCancelNote = () => {
    setEditingNoteId(null);
    setNewNoteText("");
    setNewNoteTags([]);
  };

  const handleAddTagToNote = async (noteId: number, tag: string) => {
    try {
      await addTagToNote(noteId, tag);
      onUpdate((prev) => ({
        ...prev,
        notes: prev.notes.map((note: Note) =>
          note.id === noteId
            ? { ...note, tags: [...(note.tags || []), tag] }
            : note
        ),
      }));
    } catch (error) {
      console.error("Error adding tag to note:", error);
    }
  };

  const handleStartAddTagToNote = (noteId: number) => {
    setAddingTagToNoteId(noteId);
  };

  const handleSaveTagToNote = async () => {
    if (addingTagToNoteId === null || !newTagForNote.trim()) return;
    await handleAddTagToNote(addingTagToNoteId, newTagForNote.trim());
    setNewTagForNote("");
    setAddingTagToNoteId(null);
  };

  const handleCancelTagToNote = () => {
    setNewTagForNote("");
    setAddingTagToNoteId(null);
  };

  return (
    <div className="contact-section">
      <div className="flex justify-between items-center">
        <h4>Notes:</h4>
      </div>
      <ul className="notes-list">
        {notes.map((note) => (
          <li key={note.id} className="note-item flex justify-between items-start">
            <div>
              {editingNoteId === note.id ? (
                <div className="flex flex-col gap-2">
                  <EditableInput
                    value={newNoteText}
                    onChange={setNewNoteText}
                    onSave={handleSaveNote}
                    onCancel={handleCancelNote}
                    type="textarea"
                    className=""
                  />
                </div>
              ) : (
                <>
                  <p>{note.text}</p>
                  <div className="flex flex-col gap-2 mt-2">
                    <div className="note-tags flex items-center">
                      {/* <p className="text-sm text-gray-300">Tags: </p> */}
                      {note.tags.map((tag, i) => (
                        <span key={i} className="tag note-tag">
                          {tag}
                        </span>
                      ))}
                      {addingTagToNoteId === note.id ? (
                        <TagInput
                          value={newTagForNote}
                          onChange={setNewTagForNote}
                          onSave={handleSaveTagToNote}
                          onCancel={handleCancelTagToNote}
                        />
                      ) : (
                        <AddButton
                          onAction={() => handleStartAddTagToNote(note.id)}
                          size={17}
                        />
                      )}
                    </div>
                  </div>
                </>
              )}
            </div>
            <EditButton
              onAction={() => handleEditNote(note.id, note.text, note.tags)}
            />
          </li>
        ))}
        {addingNote ? (
          <li className="note-item">
            <EditableInput
              value={newNote}
              onChange={setNewNote}
              onSave={handleSaveNewNote}
              onCancel={handleCancelNewNote}
              type="textarea"
            />
          </li>
        ) : (
          <li className="note-item">
            <AddButton onAction={handleAddNote} size={25} />
          </li>
        )}
      </ul>
    </div>
  );
};

export default NoteSection;
