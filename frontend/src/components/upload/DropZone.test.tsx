/**
 * Tests for DropZone component.
 */

import { render } from '@testing-library/react';
import { screen } from '@testing-library/dom';
import { describe, it, expect, vi } from 'vitest';
import { DropZone } from './DropZone';

describe('DropZone', () => {
  const defaultProps = {
    onFileSelect: vi.fn(),
    selectedFile: null,
    isLoading: false,
    error: null,
  };

  it('renders upload prompt when no file selected', () => {
    render(<DropZone {...defaultProps} />);
    expect(screen.getByText('common.upload')).toBeInTheDocument();
    expect(screen.getByText('common.upload_hint')).toBeInTheDocument();
  });

  it('shows file info when file is selected', () => {
    const file = new File(['content'], 'test.ifc', { type: 'application/x-step' });
    Object.defineProperty(file, 'size', { value: 1024 * 1024 * 2.5 }); // 2.5 MB

    render(<DropZone {...defaultProps} selectedFile={file} />);
    expect(screen.getByText('test.ifc')).toBeInTheDocument();
    expect(screen.getByText('2.50 MB')).toBeInTheDocument();
  });

  it('shows error message when error prop is set', () => {
    render(<DropZone {...defaultProps} error="Invalid file type" />);
    expect(screen.getByText('Invalid file type')).toBeInTheDocument();
  });

  it('shows loading state when isLoading is true', () => {
    render(<DropZone {...defaultProps} isLoading={true} />);
    expect(screen.getByText('common.validating')).toBeInTheDocument();
    expect(screen.getByText('common.loading')).toBeInTheDocument();
  });

  it('applies opacity class when loading', () => {
    const { container } = render(<DropZone {...defaultProps} isLoading={true} />);
    const dropzone = container.firstChild;
    expect(dropzone).toHaveClass('opacity-50');
    expect(dropzone).toHaveClass('cursor-not-allowed');
  });

  it('renders file input', () => {
    const { container } = render(<DropZone {...defaultProps} />);
    const input = container.querySelector('input[type="file"]');
    expect(input).toBeInTheDocument();
  });
});
