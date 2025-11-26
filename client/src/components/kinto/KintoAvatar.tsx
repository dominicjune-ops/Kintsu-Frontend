import { motion, AnimatePresence } from "framer-motion";
import { useMemo } from "react";

export type KintoState =
  | "idle"
  | "listening"
  | "thinking"
  | "responding"
  | "success"
  | "encouragement"
  | "error"
  | "loading";

interface KintoAvatarProps {
  state?: KintoState;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const SIZE_MAP = {
  sm: { container: 32, core: 20, glow: 40 },
  md: { container: 48, core: 32, glow: 60 },
  lg: { container: 64, core: 44, glow: 80 }
};

/**
 * Kinto Avatar Component
 *
 * Animated avatar with emotional intelligence
 * States: idle, listening, thinking, responding, success, encouragement, error, loading
 *
 * Design Philosophy:
 * - Calm presence (breathing idle)
 * - Warm attention (listening pulse)
 * - Golden joinery (thinking - lines converge)
 * - Confident clarity (responding expand)
 * - Gentle celebration (success ring close)
 * - Supportive lift (encouragement float)
 * - Soft reset (error reassembly)
 */
export function KintoAvatar({ state = "idle", size = "md", className = "" }: KintoAvatarProps) {
  const dimensions = SIZE_MAP[size];

  const stateConfig = useMemo(() => {
    switch (state) {
      case "listening":
        return {
          coreScale: [1, 1.1, 1],
          glowOpacity: [0.3, 0.6, 0.3],
          glowScale: [1, 1.2, 1],
          color: "from-blue-400 to-indigo-500",
          duration: 2
        };

      case "thinking":
        return {
          coreScale: [1, 0.9, 1],
          glowOpacity: [0.4, 0.8, 0.4],
          glowScale: [1, 1.3, 1],
          color: "from-accent via-amber-400 to-accent",
          duration: 1.5,
          rotate: [0, 360]
        };

      case "responding":
        return {
          coreScale: [1, 1.15, 1],
          glowOpacity: [0.5, 0.9, 0.5],
          glowScale: [1, 1.4, 1],
          color: "from-accent to-amber-400",
          duration: 1
        };

      case "success":
        return {
          coreScale: [1, 1.2, 1],
          glowOpacity: [0.6, 1, 0.3],
          glowScale: [1, 1.5, 1],
          color: "from-green-400 to-emerald-500",
          duration: 0.8
        };

      case "encouragement":
        return {
          coreScale: [1, 1.1, 1.05],
          glowOpacity: [0.4, 0.7, 0.4],
          glowScale: [1, 1.3, 1.2],
          color: "from-accent to-amber-300",
          duration: 1.2,
          y: [0, -4, 0]
        };

      case "error":
        return {
          coreScale: [1, 0.95, 1],
          glowOpacity: [0.3, 0.5, 0.3],
          glowScale: [1, 1.1, 1],
          color: "from-orange-400 to-amber-500",
          duration: 1
        };

      case "loading":
        return {
          coreScale: 1,
          glowOpacity: [0.3, 0.6, 0.3],
          glowScale: [1, 1.2, 1],
          color: "from-accent to-amber-400",
          duration: 2,
          rotate: [0, 360]
        };

      case "idle":
      default:
        return {
          coreScale: [1, 1.05, 1],
          glowOpacity: [0.2, 0.4, 0.2],
          glowScale: [1, 1.1, 1],
          color: "from-accent/80 to-amber-400/60",
          duration: 4
        };
    }
  }, [state]);

  return (
    <div
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: dimensions.container, height: dimensions.container }}
    >
      {/* Outer Glow */}
      <motion.div
        className={`absolute inset-0 rounded-full bg-gradient-to-br ${stateConfig.color} blur-xl`}
        animate={{
          opacity: stateConfig.glowOpacity,
          scale: stateConfig.glowScale,
        }}
        transition={{
          duration: stateConfig.duration,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        style={{
          width: dimensions.glow,
          height: dimensions.glow,
          left: "50%",
          top: "50%",
          transform: "translate(-50%, -50%)"
        }}
      />

      {/* Core Orb */}
      <motion.div
        className={`relative rounded-full bg-gradient-to-br ${stateConfig.color} shadow-lg`}
        animate={{
          scale: stateConfig.coreScale,
          rotate: stateConfig.rotate || 0,
          y: stateConfig.y || 0
        }}
        transition={{
          duration: stateConfig.duration,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        style={{
          width: dimensions.core,
          height: dimensions.core
        }}
      >
        {/* Inner shimmer effect */}
        <motion.div
          className="absolute inset-0 rounded-full bg-gradient-to-br from-white/40 via-transparent to-transparent"
          animate={{
            rotate: [0, 360]
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "linear"
          }}
        />

        {/* Kintsugi-inspired lines (thinking state) */}
        <AnimatePresence>
          {state === "thinking" && (
            <svg
              className="absolute inset-0 w-full h-full"
              viewBox="0 0 32 32"
            >
              <motion.path
                d="M16 4 L16 28 M4 16 L28 16 M8 8 L24 24 M24 8 L8 24"
                stroke="rgba(255, 255, 255, 0.6)"
                strokeWidth="1"
                fill="none"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: [0, 1, 0] }}
                exit={{ pathLength: 0, opacity: 0 }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
            </svg>
          )}
        </AnimatePresence>

        {/* Success ring */}
        <AnimatePresence>
          {state === "success" && (
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-white/80"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: [0.8, 1.2, 1], opacity: [0, 1, 0] }}
              exit={{ scale: 1.2, opacity: 0 }}
              transition={{ duration: 0.8 }}
            />
          )}
        </AnimatePresence>
      </motion.div>

      {/* Particle effects for special states */}
      <AnimatePresence>
        {(state === "success" || state === "encouragement") && (
          <>
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-1 h-1 rounded-full bg-accent"
                initial={{
                  x: 0,
                  y: 0,
                  opacity: 1,
                  scale: 0
                }}
                animate={{
                  x: Math.cos((i * Math.PI * 2) / 6) * 20,
                  y: Math.sin((i * Math.PI * 2) / 6) * 20,
                  opacity: [1, 0],
                  scale: [0, 1, 0]
                }}
                exit={{ opacity: 0, scale: 0 }}
                transition={{
                  duration: 1,
                  delay: i * 0.1
                }}
                style={{
                  left: "50%",
                  top: "50%"
                }}
              />
            ))}
          </>
        )}
      </AnimatePresence>
    </div>
  );
}

// Preset avatar compositions for common use cases
export function KintoAvatarListening() {
  return <KintoAvatar state="listening" size="md" />;
}

export function KintoAvatarThinking() {
  return <KintoAvatar state="thinking" size="md" />;
}

export function KintoAvatarSuccess() {
  return <KintoAvatar state="success" size="md" />;
}
