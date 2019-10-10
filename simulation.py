import random, sys
import uuid
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        self.logger = Logger(f"{virus.name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt")
        self.virus = virus
        self.pop_size = pop_size
        self.initial_infected = initial_infected
        self.vacc_percentage = vacc_percentage
        self.population = self._create_population(initial_infected)
        self.newly_infected = []
        self.current_infected = self.initial_infected
        self.total_infected = initial_infected
        self.total_vacc = int(vacc_percentage*self.pop_size)
        self.num_people_vacc_saved = 0
        self.total_dead = 0

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.
            Returns:
                list: A list of Person objects.
        '''
        infected_population = [Person(uuid.uuid4(), False, self.virus) for _ in range(0, initial_infected)]
        pop_vacc_percentage = int((self.pop_size*self.vacc_percentage))
        vacc_population = [Person(uuid.uuid4(), True) for _ in range(0, pop_vacc_percentage)]
        normal_population = [Person(uuid.uuid4(), False) for _ in range(0, self.pop_size-len(vacc_population)-len(infected_population))]
        population = infected_population+vacc_population+normal_population
        assert len(population) == self.pop_size
        return population

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        if self.total_vacc+self.total_dead == self.pop_size or self.current_infected == 0:
            return False
        else:
            return True

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            print(f'Time Step: {time_step_counter}')
            self.time_step()
            time_step_counter += 1
            should_continue = self._simulation_should_continue()
            self.logger.log_time_step(time_step_counter)
        print(f'The simulation has ended after {time_step_counter} turns.')
        print(f'Pop Size: {self.pop_size}, Vacc Percentage: {self.vacc_percentage}')
        print(f'Infection: {self.virus.name}, Repo Rate: {self.virus.repro_rate}, Mortality Rate: {self.virus.mortality_rate}')
        print(f'People Infected Percent: {self.total_infected/self.pop_size}')
        print(f'Total Dead: {self.total_dead}')
        print(f'Saved by Vaccination: {self.num_people_vacc_saved}')

    def time_step(self):
        '''This method should contain all the logic for computing one time step in the simulation.
                This includes:
                    1. 100 total interactions with a randon person for each infected person
                        in the population
                    2. If the person is dead, grab another random person from the population.
                        Since we don't interact with dead people, this does not count as an interaction.
                    3. Otherwise call simulation.interaction(person, random_person) and
                        increment interaction counter by 1.'''
        people_alive = [person for person in self.population if person.is_alive]
        for person in self.population:
            if person.infection and person.is_alive:
                interaction_count = 0
                while interaction_count < 100:
                    random_person = random.choice(people_alive)
                    if random_person.is_alive and random_person != person: 
                        self.interaction(person, random_person)
                        interaction_count += 1
        self._did_infected_survive()
        self._infect_newly_infected()

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.
            Args:
                person1 (person): The initial infected person
                random_person (person): The person that person1 interacts with.'''
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated is False and random_person.infection is None \
             and random_person._id not in self.newly_infected:
            chance = random.randint(0, 100)/100
            if chance < self.virus.repro_rate:
                self.total_infected += 1
                self.current_infected += 1
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, None, None, True)
            else:
                self.logger.log_interaction(person, random_person)
        elif random_person.is_vaccinated is True:
            self.num_people_vacc_saved += 1
            self.logger.log_interaction(person, random_person, None, True, None)
        elif random_person.infection or random_person._id in self.newly_infected:
            self.logger.log_interaction(person, random_person, True)
        else:
            print('An error occured during interaction')

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        for person in self.population:
            if person._id in self.newly_infected:
                person.infection = self.virus
        self.newly_infected = []

    def _did_infected_survive(self):
        ''' This method interate over the infected population and 
        calls did_survive_infection on them'''
        for person in self.population:
            if person.infection:
                did_survive = person.did_survive_infection()
                if did_survive is False: self.total_dead += 1
                if did_survive is True: self.total_vacc += 1
                self.current_infected -= 1
                self.logger.log_infection_survival(person, did_survive)

def test_calculations(self):
    for person in self.population:
        if person.infection and person.is_alive and person.is_vaccinated is True:
            print(person)

if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0]).replace(' ', '-')
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()
