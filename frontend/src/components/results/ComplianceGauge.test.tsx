/**
 * Tests for ComplianceGauge component.
 */

import { render } from '@testing-library/react';
import { screen } from '@testing-library/dom';
import { describe, it, expect } from 'vitest';
import { ComplianceGauge } from './ComplianceGauge';

describe('ComplianceGauge', () => {
  it('displays the correct percentage', () => {
    render(<ComplianceGauge percentage={85} label="Test Label" />);
    expect(screen.getByText('85%')).toBeInTheDocument();
  });

  it('displays the label', () => {
    render(<ComplianceGauge percentage={85} label="Test Label" />);
    expect(screen.getByText('Test Label')).toBeInTheDocument();
  });

  it('rounds percentage to whole number', () => {
    render(<ComplianceGauge percentage={85.7} label="Test" />);
    expect(screen.getByText('86%')).toBeInTheDocument();
  });

  it('clamps percentage to 0-100 range', () => {
    const { rerender } = render(<ComplianceGauge percentage={-10} label="Test" />);
    expect(screen.getByText('0%')).toBeInTheDocument();

    rerender(<ComplianceGauge percentage={150} label="Test" />);
    expect(screen.getByText('100%')).toBeInTheDocument();
  });

  it('renders SVG with correct structure', () => {
    const { container } = render(<ComplianceGauge percentage={50} label="Test" />);
    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();

    const circles = container.querySelectorAll('circle');
    expect(circles.length).toBe(2); // Background and progress circles
  });

  it('applies green color for high compliance (>= 90%)', () => {
    render(<ComplianceGauge percentage={95} label="High" />);
    const percentageText = screen.getByText('95%');
    expect(percentageText).toHaveClass('text-green-500');
  });

  it('applies amber color for medium compliance (70-89%)', () => {
    render(<ComplianceGauge percentage={75} label="Medium" />);
    const percentageText = screen.getByText('75%');
    expect(percentageText).toHaveClass('text-amber-500');
  });

  it('applies red color for low compliance (< 70%)', () => {
    render(<ComplianceGauge percentage={50} label="Low" />);
    const percentageText = screen.getByText('50%');
    expect(percentageText).toHaveClass('text-red-500');
  });

  it('renders different sizes correctly', () => {
    const { container, rerender } = render(
      <ComplianceGauge percentage={50} label="Small" size="sm" />
    );
    let svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '80');

    rerender(<ComplianceGauge percentage={50} label="Medium" size="md" />);
    svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '120');

    rerender(<ComplianceGauge percentage={50} label="Large" size="lg" />);
    svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '160');
  });
});
