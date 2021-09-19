class Assignment:
    """
    Here we define the Assignment
    """
    def __init__(self, assignment_id, description, deadline):
        self._id = assignment_id
        self._description = description
        self._deadline = deadline

    @property
    def id(self):
        """
        Get id (type: string)
        """
        return self._id

    @property
    def description(self):
        """
        Get description (type: string)
        """
        return self._description

    @property
    def deadline(self):
        """
        Get deadline (type: list of strings)
        """
        return self._deadline

    @property
    def deadline_day(self):
        """
        Get deadline day (type: string)
        """
        return self._deadline[0]

    @property
    def deadline_month(self):
        """
        Get deadline month (type: string)
        """
        return self._deadline[1]

    def set_id(self, id):
        """
        Set id
        :param id: (type: string)
        """
        self._id = id

    def set_description(self, descr):
        """
        Set description
        :param descr: (type: string)
        """
        self._description = descr

    def set_deadline(self, deadline):
        """
        Set deadline
        :param deadline: (type: list of strings)
        """
        self._deadline = deadline

    def set_deadline_day(self, day):
        """
        Set deadline day
        :param day: (type: string)
        """
        self._deadline[0] = day

    def set_deadline_month(self, month):
        """
        Set deadline month
        :param month: (type: string)
        """
        self._deadline[1] = month
