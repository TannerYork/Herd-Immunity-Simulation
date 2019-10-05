class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        log_file = open(self.file_name, 'w+')
        log_file.write(f'{pop_size} {vacc_percentage} {virus_name} {mortality_rate} {basic_repro_num}\n')
        log_file.close()

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        log_file = open(self.file_name, 'a+')
        if random_person_sick is None and random_person_vacc is None and did_infect is None:
            log_file.write(f"{person._id} didn't infect {random_person._id} because chance greater than repo_rate\n")
        elif did_infect is None and random_person_sick is True:
            log_file.write(f"{person._id} didn't infect {random_person._id} because already sick\n")
        elif did_infect is None and random_person_vacc is True:
            log_file.write(f"{person._id} didn't infect {random_person._id} because vaccinated\n")
        elif did_infect is True:
            log_file.write(f"{person._id} infects {random_person._id}\n")
        log_file.close()

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        log_file = open(self.file_name, 'a+')
        if did_die_from_infection:
            log_file.write(f'{person._id} survived infection\n')
        else:
            log_file.write(f'{person._id} died from infection\n')
        log_file.close()

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
        log_file = open(self.file_name, 'a+')
        log_file.write(f'Time step {time_step_number} ended, beginning {time_step_number + 1}\n')
        log_file.close()