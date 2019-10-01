from person import Person
from virus import Virus


class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = None

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        pass

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        pass

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        pass

    def log_time_step(self, time_step_number):
        ''' STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        pass


#### Test Logger Class ####
sample_logger = Logger('sample-file')
sample_virus = Virus('Ebola', 0.25, 0.70)
sample_person = Person(1, False)
sample_infected = Person(2, False, sample_virus)
sample_imune = Person(3, True)

def test_wite_metadata():
    sample_logger.write_metadata(10000, 0.90, sample_virus.name, sample_virus.mortality_rate, sample_virus.repro_rate)
    sample_file = open(sample_logger.file_name, 'r')
    assert sample_file.readlines()[0] == f'1000 0.90 {sample_virus.name} {sample_virus.mortality_rate} {sample_virus.repro_rate} 10'
    sample_file.close()

def test_log_interaction():
    sample_file = open(sample_logger.file_name, 'r')
    sample_logger.log_interaction(sample_infected, sample_infected, True)
    assert sample_file.readlines()[1] == f"{sample_infected._id} didn't infect {sample_infected._id} because already sick"
    sample_logger.log_interaction(sample_infected, sample_person, False, False, True)
    assert sample_file.readlines()[2] == f"{sample_infected._id} infects {sample_person._id}"
    sample_logger.log_interaction(sample_infected, sample_imune, False, True, False)
    assert sample_file.readlines()[3] == f"{sample_infected._id} didn't infect {sample_imune._id} because vaccinated"
    sample_file.close()

def test_log_infection_survival():
    sample_file = open(sample_logger.file_name, 'r')
    sample_logger.log_infection_survival(sample_person, True)
    assert sample_file.readlines()[4] == f'{sample_person._id} died from infection'
    sample_logger.log_infection_survival(sample_person, False)
    assert sample_file.readlines()[5] == f'{sample_person._id} survived infection.'
    sample_file.close()

def test_log_time_step():
    sample_file = open(sample_logger.file_name, 'r')
    sample_logger.log_time_step(1)
    assert sample_file.readlines()[6] == f'Time step 1 ended, beginning 2'
    sample_file.close()