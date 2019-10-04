from logger import Logger
from person import Person
from virus import Virus

#### Test Logger Class ####
sample_logger = Logger('sample-file.txt')
sample_virus = Virus('Ebola', 0.25, 0.70)
sample_person = Person(1, False)
sample_infected = Person(2, False, sample_virus)
sample_imune = Person(3, True)

def test_wite_metadata():
    sample_logger.write_metadata(10000, 0.9, sample_virus.name, sample_virus.mortality_rate, sample_virus.repro_rate)
    sample_file = open(sample_logger.file_name, 'r')
    assert sample_file.readlines()[0] == f'10000 0.9 {sample_virus.name} {sample_virus.mortality_rate} {sample_virus.repro_rate}\n'
    sample_file.close()

def test_log_interaction():
    sample_file = open(sample_logger.file_name, 'r')
    sample_logger.log_interaction(sample_infected, sample_infected, True)
    assert sample_file.readlines()[1] == f"{sample_infected._id} didn't infect {sample_infected._id} because already sick\n"
    sample_logger.log_interaction(sample_infected, sample_person, None, None, True)
    assert sample_file.readlines()[0] == f"{sample_infected._id} infects {sample_person._id}\n"
    sample_logger.log_interaction(sample_infected, sample_imune, None, True, None)
    assert sample_file.readlines()[0] == f"{sample_infected._id} didn't infect {sample_imune._id} because vaccinated\n"
    sample_file.close()

def test_log_infection_survival():
    sample_file = open(sample_logger.file_name, 'r')
    sample_logger.log_infection_survival(sample_person, True)
    assert sample_file.readlines()[4] == f'{sample_person._id} survived infection\n'
    sample_logger.log_infection_survival(sample_person, False)
    assert sample_file.readlines()[0] == f'{sample_person._id} died from infection\n'
    sample_file.close()

def test_log_time_step():
    sample_file = open(sample_logger.file_name, 'r')
    sample_logger.log_time_step(1)
    assert sample_file.readlines()[6] == f'Time step 1 ended, beginning 2\n'
    sample_file.close()