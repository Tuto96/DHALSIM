from abc import ABCMeta, abstractmethod


class Attack:
    """Defines an attack executed by a PLC (device or network attack)

    :param name: The name of the attack
    """
    __metaclass__ = ABCMeta

    def __init__(self, name, actuators, command):
        self.name = name
        self.actuators = actuators
        self.command = command

    @abstractmethod
    def apply(self, plc):
        """Applies an attack rule using a given PLC

        :param plc: the PLC that will apply the attack
        """
        pass


class DeviceAttack(Attack):
    """
    Defines a Device Attack, which is an attack that will perform an action on a given PLC

    :param name: The name of the attack
    :param actuators: The actuators that will be attacked
    :param command: The command to execute on the actuators
    :param start: The start time of the attack
    :param end: The end time of the attack
    """
    def __init__(self, name, actuators, command, start, end):
        super(DeviceAttack, self).__init__(name, actuators, command)
        self.start = start
        self.end = end

    def apply(self, plc):
        """Applies the Device Attack on a given PLC

        :param plc: The PLC that will apply the action
        """
        curr_time = plc.get_master_clock()
        print("Checking attack time: " + str(curr_time))
        if self.start <= curr_time <= self.end:
            print("Attack applied")
            for actuator in self.actuators:
                plc.set_tag(actuator, self.command)

class TriggerBelowAttack(Attack):
    """
    Defines an attack that is executed on a certain trigger. A trigger is a tag going below a certain value
    For example, we can define an attack that starts when a tank level drops below a given value

    :param name: The name of the attack
    :param actuators: The actuators that will be attacked
    :param command: The command to execute on the actuators
    :param trigger: The tag that will be used as the trigger
    :param value: The value that will be compared to the value of the trigger
    """
    def __init__(self, name, actuators, command, trigger, value):
        super(TriggerBelowAttack, self).__init__(name, actuators, command)
        self.trigger = trigger
        self.value = value

    def apply(self, plc):
        """
        Applies the TriggerAttack when necessary

        :param plc: The PLC that will apply the action
        """
        trigger_value = plc.get_tag(self.trigger)
        if trigger_value < self.value:
            for actuator in self.actuators:
                plc.set_tag(actuator, self.command)

class TriggerAboveAttack(Attack):
    """
    Defines an attack that is executed on a certain trigger. A trigger is a tag going above a certain value
    For example, we can define an attack that starts when a tank level goes above a given value

    :param name: The name of the attack
    :param actuators: The actuators that will be attacked
    :param command: The command to execute on the actuators
    :param trigger: The tag that will be used as the trigger
    :param value: The value that will be compared to the value of the trigger
    """

    def __init__(self, name, actuators, command, trigger, value):
        super(TriggerAboveAttack, self).__init__(name, actuators, command)
        self.trigger = trigger
        self.value = value

    def apply(self, plc):
        """
        Applies the TriggerAttack when necessary

        :param plc: The PLC that will apply the action
        """
        trigger_value = plc.get_tag(self.trigger)
        if trigger_value > self.value:
            for actuator in self.actuators:
                plc.set_tag(actuator, self.command)