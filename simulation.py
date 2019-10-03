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
        self.pop_size = pop_size
        self.next_person_id = 0
        self.virus = virus
        self.initial_infected = initial_infected
        self.total_infected = 0
        self.current_infected = initial_infected
        self.vacc_percentage = vacc_percentage
        self.population = self._create_population(initial_infected)
        self.newly_infected = [person._id for person in self.population if person.infection]
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
        return infected_population + vacc_population + normal_population

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        num_vacc = sum(1 for person in self.population if person.is_vaccinated)
        if self.current_infected == self.pop_size or num_vacc == self.pop_size:
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
            self.time_step()
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
        print(f'The simulation has ended after {time_step_counter} turns.')

    def time_step(self):
        '''This method should contain all the logic for computing one time step in the simulation.
                This includes:
                    1. 100 total interactions with a randon person for each infected person
                        in the population
                    2. If the person is dead, grab another random person from the population.
                        Since we don't interact with dead people, this does not count as an interaction.
                    3. Otherwise call simulation.interaction(person, random_person) and
                        increment interaction counter by 1.'''
        infected_persons = [person for person in self.population if person.infection and person.is_alive]
        for infected in infected_persons:
            for _ in range(101):
                person = random.choice(self.population)
                while person.is_alive is False and self.total_dead != self.pop_size:
                    person = random.choice(self.population)
                self.interaction(infected, person)

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.
            Args:
                person1 (person): The initial infected person
                random_person (person): The person that person1 interacts with.'''
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated is False and random_person.infection is None:
            chance = random.randint(0, 100)/100
            if chance < self.virus.repro_rate:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, did_infect=True)
        elif random_person.is_vaccinated is True:
            self.logger.log_interaction(person, random_person, random_person_vacc=True)
        elif random_person.infection is not None:
            self.logger.log_interaction(person, random_person, random_person_sick=True)
        else:
            print('An error occured during interaction')

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        needs_to_be_inffected = [person for person in self.population if person._id in self.newly_infected] 
        for person in needs_to_be_inffected:
            person.infection = self.virus
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()
