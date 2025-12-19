import React from 'react';
import { cn, pills, textStyles } from '../../../shared/ui';

function RelatedFilesList({ uploadedFiles }) {
  if (!uploadedFiles || uploadedFiles.length === 0) {
    return <div className={cn(textStyles.muted, "text-center")}>No related files</div>;
  }

  return (
    <ul className="flex flex-wrap list-none gap-2 p-0 mt-3">
      {uploadedFiles.map((file, index) => (
        <li
          key={`${file.name || 'file'}-${index}`}
          className={cn(pills.fileItem, pills.fileItemLoose)}
        >
          <a
            href={file.url}
            target="_blank"
            rel="noreferrer"
            className="text-ink font-semibold transition-colors hover:text-brand-purple focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-purple/40"
          >
            {file.name || 'Untitled files'}
          </a>{' '}
          <span className={pills.source}>
            {file.source}
          </span>
        </li>
      ))}
    </ul>
  );
}

export default RelatedFilesList;
