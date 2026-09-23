from data_generator import generate_fitness_data


class ReferenceProfile:
    def __init__(self, baseline_heart_rate, baseline_skin_response, baseline_temperature):
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

class Participant:
    def __init__(self, participant_id, reference_profile):
        self.participant_id = participant_id
        self.reference_profile = reference_profile


class Observation:
    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

    @classmethod
    def from_dict(cls, d):
        return cls(
            data["timestamp"],
            data["heart_rate"],
            data["skin_response"],
            data["temperature"],
            data["activity_level"],
            data["signal_quality"]
        )

    def is_valid(self):
        if not valid_heart_rate(self.heart_rate):
            return False

        if not valid_skin_response(self.skin_response):
            return False

        if not valid_temperature(self.temperature):
            return False

        if not valid_activity_level(self.activity_level):
            return False

        if not valid_signal_quality(self.signal_quality):
            return False

        return True


class FitnessSession:
    def __init__(self, participant):
        self.participant = participant
        self._observations = []

    def add_observation(self, observation):
        self._observations.append(observation)

    @property
    def observations(self):
        return self._observations

def valid_heart_rate(heart_rate):
    if heart_rate is None:
        return False
    if heart_rate < 35 or heart_rate > 205:
        return False
    return True

def valid_temperature(temperature):
    if temperature is None:
        return False
    if temperature < 25 or temperature > 42:
        return False
    return True

def valid_activity_level(activity_level):
    if activity_level is None:
        return False
    if activity_level < 0 or activity_level > 1:
        return False
    return True

def valid_signal_quality(signal_quality):
    if signal_quality is None:
        return False
    if signal_quality < 0 or signal_quality > 1:
        return False
    return True

def valid_skin_response(skin_response):
    if skin_response is None:
        return False
    if skin_response < 0:
        return False
    return True

def calculate_average(values):
    if len(values) == 0:
        return None
    return sum(values) / len(values)

def calculate_minimum(values):
    if len(values) == 0:
        return None

    return min(values)

def calculate_maximum(values):
    if len(values) == 0:
        return None
    return max(values)

def classify_session(average_activity, heart_rate_difference):
    if average_activity < 0.3 and heart_rate_difference < 20:
        return "resting"
    if average_activity < 0.68 and heart_rate_difference < 50:
        return "moderate activity"

    return "high activity"

def is_recovering(valid_observations):
    if len(valid_observations) <4:
        return False

    first_heart_rate = valid_observations[0].heart_rate
    last_heart_rate = valid_observations[-1].heart_rate

    first_activity = valid_observations[0].activity_level
    last_activity = valid_observations[-1].activity_level

    heart_rate_decreased = last_heart_rate < first_heart_rate
    activity_decreased = last_activity < first_activity

    return heart_rate_decreased and activity_decreased

def create_result(
        session,
        classification,
        valid_count,
        invalid_count,
        average_heart_rate,
        valid_heart_rates,
        baseline_heart_rate,
        heart_rate_difference,
        average_activity
):
    return {
        "participant_id": session.participant.participant_id,
        "classification": classification,
        "valid_observations": valid_count,
        "invalid_observations": invalid_count,
        "average_heart_rate": average_heart_rate,
        "minimum_heart_rate": calculate_minimum(valid_heart_rates),
        "maximum_heart_rate": calculate_maximum(valid_heart_rates),
        "baseline_heart_rate": baseline_heart_rate,
        "heart_rate_difference": heart_rate_difference,
        "average_activity": average_activity,
    }

def print_report(result):
    print()
    print("----- FITNESS SESSION REPORT -----")
    print("Participant:", result["participant_id"])
    print("Classification:", result["classification"])
    print("valid observations:", result["valid_observations"])
    print("invalid observations:", result["invalid_observations"])
    print()
    print("Average heart rate:", display_value(result["average_heart_rate"]))
    print("Minimum heart rate:", display_value(result["minimum_heart_rate"]))
    print("Maximum heart rate:", display_value(result["maximum_heart_rate"]))
    print("Baseline heart rate:", display_value(result["baseline_heart_rate"]))
    print("heart rate difference:", display_value(result["heart_rate_difference"]))
    print("Average activity:", display_value(result["average_activity"]))
    print("----------------------------------")

def display_value(value):
        if value is None:
            return "N/A"
        return value


profile, observations = generate_fitness_data(
    participant_id= "P001",
    scenario= "poor_quality",
    seed= 42,
    number_of_windows= 12
)


reference_profile = ReferenceProfile(
    profile["baseline_heart_rate"],
    profile["baseline_skin_response"],
    profile["baseline_temperature"]
)

participant = Participant(
    profile["participant_id"],
    reference_profile
)

session = FitnessSession(participant)



for data in observations:
    observation = Observation.from_dict(data)
    session.add_observation(observation)

valid_count = 0
invalid_count = 0
valid_observations = []

for observation in session.observations:
    if observation.is_valid():
        valid_count += 1
        valid_observations.append(observation)
    else:
        invalid_count += 1


print("valid observations:", valid_count)
print("invalid observations:", invalid_count)


print("Participants", session.participant.participant_id)
print("Number of observations:", len(session.observations))

valid_heart_rates = []

for observation in session.observations:
    if observation.is_valid():
        valid_heart_rates.append(observation.heart_rate)


print("Average heart rate:", calculate_average(valid_heart_rates))
print("Minimum heart rate:", calculate_minimum(valid_heart_rates))
print("Maximum heart rate:", calculate_maximum(valid_heart_rates))

valid_activity_levels = []

for observation in session.observations:
    if observation.is_valid():
        valid_activity_levels.append(observation.activity_level)

print("Average activity level:", calculate_average(valid_activity_levels))

average_heart_rate = calculate_average(valid_heart_rates)
baseline_heart_rate = session.participant.reference_profile.baseline_heart_rate


if average_heart_rate is None:
    heart_rate_difference = None
else:
    heart_rate_difference = (average_heart_rate - baseline_heart_rate)

print("baseline heart rate:", baseline_heart_rate)
print("heart rate above baseline:", heart_rate_difference)

average_activity = calculate_average(valid_activity_levels)


if len(valid_observations) < 4:
    classification = "insufficient data"

elif is_recovering(valid_observations):
    classification = "recovering"

else:
    classification = classify_session(
        average_activity,
        heart_rate_difference
    )

print("session classification:", classification)

results = create_result(
    session,
    classification,
    valid_count,
    invalid_count,
    average_heart_rate,
    valid_heart_rates,
    baseline_heart_rate,
    heart_rate_difference,
    average_activity
)

print_report(results)



