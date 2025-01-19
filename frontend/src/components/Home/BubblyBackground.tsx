import { useEffect, useRef } from 'react';

interface Bubble {
  x: number;
  y: number;
  radius: number;
  speed: number;
  opacity: number;
}

const BubblyBackground = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const bubbles = useRef<Bubble[]>([]);
  const animationFrameId = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const createBubbles = () => {
      const numberOfBubbles = 50;
      bubbles.current = Array.from({ length: numberOfBubbles }, () => ({
        x: Math.random() * canvas.width,
        y: canvas.height + Math.random() * 20,
        radius: Math.random() * 30 + 10,
        speed: Math.random() * 1.5 + 0.5,
        opacity: Math.random() * 0.3 + 0.2,
      }));
    };

    const drawBubble = (bubble: Bubble) => {
      if (!ctx) return;

      ctx.beginPath();
      const gradient = ctx.createRadialGradient(
        bubble.x,
        bubble.y,
        0,
        bubble.x,
        bubble.y,
        bubble.radius
      );
      gradient.addColorStop(0, `rgba(36, 36, 36, ${bubble.opacity * 1.5})`);
      gradient.addColorStop(1, 'rgba(36, 36, 36, 0)');
      
      ctx.fillStyle = gradient;
      ctx.arc(bubble.x, bubble.y, bubble.radius, 0, Math.PI * 2);
      ctx.fill();
    };

    const animate = () => {
      if (!ctx || !canvas) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      bubbles.current.forEach((bubble, index) => {
        bubble.y -= bubble.speed;

        if (bubble.y + bubble.radius < 0) {
          bubble.y = canvas.height + bubble.radius;
          bubble.x = Math.random() * canvas.width;
        }

        drawBubble(bubble);
      });

      animationFrameId.current = requestAnimationFrame(animate);
    };

    resizeCanvas();
    createBubbles();
    animate();

    window.addEventListener('resize', () => {
      resizeCanvas();
      createBubbles();
    });

    return () => {
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
      }}
    />
  );
};

export default BubblyBackground;
