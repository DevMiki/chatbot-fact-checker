import React, { useState } from 'react';
import { buttons, cn, inputs, pills, textStyles } from '../../../shared/ui';

const ALLOWED_EXTENSIONS = ['pdf'];
const ALLOWED_MIME_TYPES = ['application/pdf'];

const isAllowedFile = (file) => {
  const name = (file?.name || '').toLowerCase();
  const mimeType = (file?.type || '').toLowerCase();

  const lastDot = name.lastIndexOf('.');
  const extension = lastDot > 0 ? name.slice(lastDot + 1) : '';

  return (
    ALLOWED_EXTENSIONS.includes(extension) &&
    (!mimeType || ALLOWED_MIME_TYPES.includes(mimeType))
  );
};

function ChatInput({
  question,
  files,
  useLlm,
  onQuestionChange,
  onFilesChange,
  onUseLlmChange,
  onSubmit,
  loading,
  fileInputKey,
}) {
  const [invalidFiles, setInvalidFiles] = useState([]);

  const handleNewFiles = (incomingFiles) => {
    const validFiles = [];
    const invalidUploads = [];

    incomingFiles.forEach((file) => {
      if (isAllowedFile(file)) {
        validFiles.push(file);
      } else {
        invalidUploads.push(file.name || 'Invalid file');
      }
    });

    if (validFiles.length) {
      onFilesChange([...files, ...validFiles]);
    }

    setInvalidFiles(invalidUploads);
  };

  const handleFileChange = (event) => {
    const incomingFiles = Array.from(event.target.files || []);
    handleNewFiles(incomingFiles);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const dropped = Array.from(event.dataTransfer.files || []);
    if (dropped.length === 0) return;
    handleNewFiles(dropped);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleRemoveFile = (indexToRemove) => {
    onFilesChange(files.filter((_, idx) => idx !== indexToRemove));
  };

  return (
    <form className="flex flex-col gap-5 text-ink" onSubmit={onSubmit}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className={textStyles.caption}>Step 1</p>
          <h2 className="mt-1 text-ink text-lg font-bold">Ask your question</h2>
          <p className={textStyles.subtext}>Share context and attach PDFs if you want them referenced.</p>
        </div>
        <div className="flex items-center gap-3">
          <span className={textStyles.label}>Use LLM</span>
          <button
            type="button"
            role="switch"
            aria-checked={useLlm}
            onClick={() => onUseLlmChange?.(!useLlm)}
            className={cn(
              "relative inline-flex h-8 w-16 items-center rounded-full border-2 border-ink shadow-ink-sm transition-colors",
              useLlm ? "bg-brand-purple" : "bg-white"
            )}
          >
            <span
              className={cn(
                "ml-1 inline-block h-6 w-6 rounded-full border-2 border-ink bg-white shadow-ink-sm transition-transform",
                useLlm ? "translate-x-7" : "translate-x-0"
              )}
            />
          </button>
        </div>
      </div>

      <label className="flex flex-col gap-2">
        <div className="flex items-center justify-between gap-3">
          <span className={textStyles.label}>Question</span>
          <span className={textStyles.subtext} title="Enter sends, Shift+Enter adds a new line">
            ⏎ to send · ⇧⏎ new line
          </span>
        </div>
        <textarea
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="e.g., Is Pizza simply the best food ever created?"
          required
          className={inputs.textarea}
          onKeyDown={(event) => {
            if(event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault();
              event.currentTarget.form.requestSubmit()
            }
          }}
        />
      </label>

      <label className="flex flex-col gap-2">
        <span className={textStyles.label}>Attach PDFs (optional)</span>
        <div
          className={inputs.dropzone}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className={cn('m-0', textStyles.label)}>Drag & drop PDFs here</p>
              <p className={cn('m-0', textStyles.subtext)}>or choose files to upload</p>
            </div>
            <label className={buttons.upload}>
              <input
                key={fileInputKey}
                type="file"
                accept=".pdf"
                multiple
                onChange={handleFileChange}
                className="absolute inset-0 cursor-pointer opacity-0"
              />
              Browse PDFs
            </label>
          </div>
          {files.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {files.map((file, idx) => (
                <span
                  key={`${file.name}-${idx}`}
                  className={cn(pills.fileItem, pills.fileItemCompact)}
                >
                  <span className="truncate max-w-xs">{file.name}</span>
                  <button
                    type="button"
                    onClick={(event) => {
                      event.preventDefault();
                      event.stopPropagation();
                      handleRemoveFile(idx);
                    }}
                    className={buttons.icon}
                    aria-label={`Remove ${file.name}`}
                  >
                    x
                  </button>
                </span>
              ))}
            </div>
          )}
          {invalidFiles.length > 0 && (
            <p className={cn('mt-2', textStyles.warning)}>
              Ignored non-PDF files: {invalidFiles.join(', ')}
            </p>
          )}
        </div>
      </label>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading}
          className={buttons.primary}
        >
          {loading ? 'Sending...' : 'Send to chatbot'}
        </button>
      </div>
    </form>
  );
}

export default ChatInput;

