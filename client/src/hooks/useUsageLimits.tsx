import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { LimitType } from '@/components/monetization/LimitModal';

interface UsageLimits {
  resumeRepairs: number;
  coachMessages: number;
  insightReports: number;
}

interface UsageStore {
  usage: UsageLimits;
  isPro: boolean;
  incrementUsage: (type: LimitType) => boolean;
  resetUsage: () => void;
  upgradeToPro: () => void;
  checkLimit: (type: LimitType) => { isAtLimit: boolean; current: number; limit: number };
}

const LIMITS = {
  free: {
    resumeRepairs: 3,
    coachMessages: 10,
    insightReports: 2,
  },
  pro: {
    resumeRepairs: Infinity,
    coachMessages: Infinity,
    insightReports: Infinity,
  },
};

const USAGE_KEY_MAP: Record<LimitType, keyof UsageLimits> = {
  resume_repairs: 'resumeRepairs',
  coach_messages: 'coachMessages',
  insight_reports: 'insightReports',
};

export const useUsageLimits = create<UsageStore>()(
  persist(
    (set, get) => ({
      usage: {
        resumeRepairs: 0,
        coachMessages: 0,
        insightReports: 0,
      },
      isPro: false,

      incrementUsage: (type: LimitType) => {
        const state = get();
        const usageKey = USAGE_KEY_MAP[type];
        const currentUsage = state.usage[usageKey];
        const limit = state.isPro ? LIMITS.pro[usageKey] : LIMITS.free[usageKey];

        // If at limit, return false (don't increment)
        if (currentUsage >= limit) {
          return false;
        }

        // Increment usage
        set((state) => ({
          usage: {
            ...state.usage,
            [usageKey]: state.usage[usageKey] + 1,
          },
        }));

        return true;
      },

      checkLimit: (type: LimitType) => {
        const state = get();
        const usageKey = USAGE_KEY_MAP[type];
        const current = state.usage[usageKey];
        const limit = state.isPro ? LIMITS.pro[usageKey] : LIMITS.free[usageKey];

        return {
          isAtLimit: current >= limit,
          current,
          limit,
        };
      },

      resetUsage: () => {
        set({
          usage: {
            resumeRepairs: 0,
            coachMessages: 0,
            insightReports: 0,
          },
        });
      },

      upgradeToPro: () => {
        set({ isPro: true });
      },
    }),
    {
      name: 'kintsu-usage-storage',
    }
  )
);
