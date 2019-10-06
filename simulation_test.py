from simulation import Simulation
from logger import Logger
from person import Person
from virus import Virus

#### Test Simulation Class ####
def test_create_population():
    virus = Virus("HIV", 0.8, 0.3)
    sim = Simulation(1000, 0.6, virus, 20)
    population = sim._create_population(20)
    assert len(population) == 1000
    percent_vacc = sum(1 for person in population if person.is_vaccinated)/len(population)
    assert percent_vacc == 0.6
    num_infected = sum(1 for person in population if person.infection)
    assert num_infected == 20

def test_simulation_should_continue():
    virus = Virus("HIV", 0.8, 0.3)
    sim_one = Simulation(1000, 0.6, virus, 20)
    assert sim_one._simulation_should_continue() == True
    sim_two = Simulation(1000, 1, virus, 0)
    assert sim_two._simulation_should_continue() == False
    sim_three = Simulation(1000, 0.0, virus, 1000)
    assert sim_three._simulation_should_continue() == True

def test_interaction():
    virus = Virus('Black Plauge', 1.0, 0.5)
    sim = Simulation(1000, 0.6, virus, 20)
    infected_person = Person(1, False, virus)
    person = Person(2, False)
    sim.interaction(infected_person, person)
    assert person._id in sim.newly_infected

def test_infect_newly_infected():
    virus = Virus('Black Plauge', 1.0, 0.5)
    sim = Simulation(1000, 0.6, virus, 20)
    person = Person(2, False)
    sim.population.append(person)
    sim.newly_infected.append(person._id)
    sim._infect_newly_infected()
    assert person.infection == virus