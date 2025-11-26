import confetti from 'canvas-confetti';

/**
 * Celebrates a milestone completion with confetti
 * Uses Kintsu brand colors: Gold (#D4A574) and Navy (#0F172A)
 */
export const celebrateMilestone = () => {
  const colors = ['#D4A574', '#0F172A', '#F5E6D3'];

  confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 },
    colors,
    ticks: 200,
  });
};

/**
 * Celebrates a major achievement with an extended confetti blast
 */
export const celebrateMajorWin = () => {
  const colors = ['#D4A574', '#0F172A', '#F5E6D3'];

  const duration = 3000;
  const animationEnd = Date.now() + duration;
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0, colors };

  function randomInRange(min: number, max: number) {
    return Math.random() * (max - min) + min;
  }

  const interval: ReturnType<typeof setInterval> = setInterval(function() {
    const timeLeft = animationEnd - Date.now();

    if (timeLeft <= 0) {
      return clearInterval(interval);
    }

    const particleCount = 50 * (timeLeft / duration);

    confetti({
      ...defaults,
      particleCount,
      origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 }
    });
    confetti({
      ...defaults,
      particleCount,
      origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 }
    });
  }, 250);
};

/**
 * Subtle confetti for small wins
 */
export const celebrateSmallWin = () => {
  const colors = ['#D4A574', '#F5E6D3'];

  confetti({
    particleCount: 30,
    spread: 45,
    origin: { y: 0.7 },
    colors,
    ticks: 100,
    gravity: 1.2,
  });
};

/**
 * Animation config for card interactions
 */
export const cardLayoutTransition = {
  type: "spring" as const,
  stiffness: 300,
  damping: 30,
};

/**
 * Animation config for step transitions in onboarding
 */
export const stepTransition = {
  initial: { opacity: 0, x: 300 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -300 },
  transition: { duration: 0.4, ease: "easeInOut" as const }
};

/**
 * Animation config for hover interactions
 */
export const cardHoverVariants = {
  initial: { scale: 1 },
  hover: {
    scale: 1.02,
    transition: { duration: 0.2 }
  }
};

/**
 * Animation config for Signal entry/exit
 */
export const signalVariants = {
  initial: { y: -100, opacity: 0 },
  animate: {
    y: 0,
    opacity: 1,
    transition: { type: "spring" as const, bounce: 0.3 }
  },
  exit: {
    y: -100,
    opacity: 0,
    transition: { duration: 0.2 }
  }
};
