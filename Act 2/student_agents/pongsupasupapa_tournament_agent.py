#!/usr/bin/env python
"""
Tournament Agent: KiasuBOT
Student: Pongsupa Supapa
Generated: 2026-10-04 13:30:52

Evolution Details:
- Generations: 1000
- Final Fitness: N/A
- Trained against: Always Undercut, Adaptive, Prober, Random (0.7), Grim Trigger...

Strategy: nice most of the time, but hates consecutive betrays
"""

from agents import Agent, INVEST, UNDERCUT
import random


class PongsupaSupapaAgent(Agent):
    """
    KiasuBOT

    nice most of the time, but hates consecutive betrays

    Evolved Genes: [1.0, 0.27069500627420273, 1.0, 0.0, 0.8713142535785792, 0.0]
    """

    def __init__(self):
        # These genes were evolved through 1000 generations
        self.genes = [1.0, 0.27069500627420273, 1.0, 0.0, 0.8713142535785792, 0.0]

        # Required for tournament compatibility
        self.student_name = "Pongsupa Supapa"

        super().__init__(
            name="KiasuBOT",
            description="nice most of the time, but hates consecutive betrays"
        )

    def choose_action(self) -> bool:
        """
        Fuzzy Logic Time!!! Modified from Unit 04 to Fit Here

        Genes:
        [0] initial cooperation
        [1] initial strategy duration
        [2] cooperate with cooperative opponents
        [3] forgiveness
        [4] memory length
        [5] consecutive defection tolerance
        """

        # Set Genes for Easier Read
        initial_cooperation = self.genes[0]
        initial_strategy_duration = self.genes[1]
        cooperation_prob = self.genes[2] # KEEPS MAXING OUT, DO WE NEED TO CHANGE?
        forgiveness = self.genes[3]
        memory = self.genes[4]
        defection_tolerance = self.genes[5]

        # TODO: Testing Prevention against Prober
        # FROM UNIT 04: WE NEEDED A CLASSIFIER FOR MODEL, SO CHECK FOR BEHAVIOR

        # NICE FOR ROUND 1
        if self.round_num == 0:
            return INVEST

        # Stuff from Unit 04
        last = self.history[-1]

        # PUNISH IF STARTED WITH UNDERCUT
        if self.round_num == 1:
            if last == UNDERCUT:
                return UNDERCUT

            else:
                return INVEST

        # MAKE SURE WE HAVE ENOUGH HISTORY
        last_last = self.history[-2]
        first_two = self.history[:2]

        # EVALUATE THE OPPONENT AND THEIR TYPES
        if self.round_num == 2:
            # IF THEY UNDERCUT TWICE, START RETALIATING
            if last_last == UNDERCUT and last == UNDERCUT:
                self.retaliate = True
                return UNDERCUT

            # PATTERN SIGNATURE SIMILAR TO PROBER
            elif last_last == UNDERCUT and last == INVEST:
                self.retaliate = False
                return INVEST

            # STAY NICE IF THEY ARE NICE
            else:
                return INVEST

        # MAKS SURE WE HAVE ENOUGH HISTORY
        first_three = self.history[:3]

        # PATTERN CHECK NOW THAT WE HAVE ENOUGH DATA
        if first_two == [UNDERCUT, UNDERCUT]:
            # CONTINUES TO UNDERCUT
            if last == UNDERCUT:
                self.retaliate = True
                return UNDERCUT

            # FORGIVE FOR FINALLY INVESTING
            else:
                self.retaliate = False

        # CHECK FOR POOPER (i hate prober) and CHECK FOR SUS TIT-FOR-TAT
        if first_three == [UNDERCUT, INVEST, INVEST] or first_three == [UNDERCUT, INVEST, UNDERCUT]:
            # IF POOPER IS NICE THEN WE ARE NICE TOO, SINCE POOPER RUNS ON TIT FOR TAT
            # SUS STARTS WITH UNDERCUT THEN TIT-FOR-TAT COPY
            self.retaliate = False
            return INVEST

        # CHECK FOR ALWAYS UNDERCUT
        if first_three == [UNDERCUT, UNDERCUT, UNDERCUT] and INVEST not in self.history:
            self.retaliate = True
            return UNDERCUT

        # GENETIC STUFF

        # First few rounds: use initial cooperation gene
        if self.round_num < max(1, round(initial_strategy_duration * 10)):
            return random.random() < initial_cooperation

        # Check consecutive defections
        defection_limit = max(1, round(defection_tolerance * 9) + 1)

        consecutive_defections = 0

        for action in reversed(self.history):
            if action == UNDERCUT:
                consecutive_defections += 1
            else:
                break

        # FLIP TO RETALIATE AFTER TOO MANY DEFECTIONS
        if consecutive_defections >= defection_limit:
            self.retaliate = True

        # FORGIVE IF THEY COOPERATE AGAIN
        if self.history[-1] == INVEST:
            self.retaliate = False

        # RETALIATE BUT SOMETIMES FORGIVE
        if self.retaliate:
            if random.random() < forgiveness:
                self.retaliate = False
                return INVEST
            else:
                return UNDERCUT

        # Calculate memory window
        memory_length = max(1, int(memory * 10) + 1)
        recent_history = self.history[-memory_length:]
        cooperation_rate = sum(recent_history) / len(recent_history)

        # High Coop Rate
        if cooperation_rate > 0.8:
            return random.random() < cooperation_prob

        # 50-80%
        elif cooperation_rate > 0.5:
            # Mix of cooperation and defection
            coop_prob = cooperation_prob * (cooperation_rate - 0.5) * 2
            return random.random() < coop_prob

        # <50%
        else:
            # Will forgive a lot
            if random.random() < forgiveness * 0.8:
                return INVEST
            else:
                return UNDERCUT



# Convenience function for tournament loading
def get_agent():
    """Return an instance of this agent for tournament use"""
    return PongsupaSupapaAgent()


if __name__ == "__main__":
    # Test that the agent can be instantiated
    agent = get_agent()
    print(f"   Agent loaded successfully: {agent.name}")
    print(f"   Genes: {agent.genes}")
    print(f"   Description: {agent.description}")
