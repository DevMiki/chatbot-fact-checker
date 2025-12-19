import React from 'react';
import RelatedFilesList from './RelatedFilesList';
import { buttons, cn, pills, surfaces, textStyles } from '../../../shared/ui';

function ChatMessage({ message, onToggleFiles }) {
  const filesCount = message.referencedFiles?.length || 0;
  return (
    <div className={surfaces.message}>
      <div className="flex items-start justify-between gap-3 pb-3 border-b-2 border-ink/20">
        <div>
          <p className={textStyles.caption}>Question</p>
          <h3 className="mt-1 text-ink text-lg font-semibold">{message.question}</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className={pills.file}>{filesCount} related files</span>
          {message.cacheHit && <span className={pills.cache}>Cache hit</span>}
        </div>
      </div>

      <div className="mt-3">
        <p className={cn("mb-1", textStyles.label)}>Answer</p>
        <p className="text-ink/80 leading-relaxed">{message.answer}</p>
      </div>

      <button
        className={cn("mt-4", buttons.accent)}
        onClick={onToggleFiles}
      >
        Related files / Fact-check
      </button>
      {message.showFiles && <RelatedFilesList uploadedFiles={message.referencedFiles} />}
    </div>
  );
}

export default ChatMessage;
