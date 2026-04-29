export default function LogoMark({ className }: { className?: string }) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M32 10c7.2 0 13 5.8 13 13 0 3.8-1.6 7.2-4.2 9.6 5.6 2.4 9.5 8 9.5 14.4 0 8.7-7.1 15.8-15.8 15.8H29.5C20.8 62.8 13.7 55.7 13.7 47c0-6.4 3.9-12 9.5-14.4C20.6 30.2 19 26.8 19 23c0-7.2 5.8-13 13-13Z"
        fill="rgb(var(--accent))"
        opacity="0.95"
      />
      <path
        d="M24 24c0-4.4 3.6-8 8-8s8 3.6 8 8c0 1.9-.7 3.7-1.8 5.1 2.9 1.2 4.8 4 4.8 7.2 0 4.4-3.6 8-8 8h-6c-4.4 0-8-3.6-8-8 0-3.2 1.9-6 4.8-7.2C24.7 27.7 24 25.9 24 24Z"
        fill="rgb(var(--bg))"
        opacity="0.9"
      />
      <path
        d="M23.5 42.5h17"
        stroke="rgb(var(--cta))"
        strokeWidth="3"
        strokeLinecap="round"
        opacity="0.9"
      />
      <path
        d="M23.5 36.5h17"
        stroke="rgb(255 255 255 / 0.6)"
        strokeWidth="3"
        strokeLinecap="round"
        opacity="0.55"
      />
      <path
        d="M16 26c-3.7 0-6.7-3-6.7-6.7S12.3 12.6 16 12.6c3.2 0 5.9 2.2 6.5 5.2"
        stroke="rgb(255 255 255 / 0.7)"
        strokeWidth="3"
        strokeLinecap="round"
      />
      <path
        d="M48 26c3.7 0 6.7-3 6.7-6.7S51.7 12.6 48 12.6c-3.2 0-5.9 2.2-6.5 5.2"
        stroke="rgb(255 255 255 / 0.7)"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
}
