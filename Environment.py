import random

from AssetManager import assetManager

AssetManager = assetManager(transform_scale=64)

class Environment:

    def __init__(self, start_time=1000, time_increment=2, rain_frequency=0.001):
        self.time = start_time
        self.time_increment = time_increment
        self.night_opacity = 100
        self.rain_frequency = rain_frequency
        self.time_string = ""
        self.max_opacity = 255
        self.current_weather = None
        self.random_value = None
        self.current_sprite = 0
        self.weather_image = None

        # frame counts
        self.rain_frame_count = 8

        # frame speed
        self.rain_frame_speed = 0.2

    def format_time(self, time):
        formatted_time = "{:02d}:{:02d}".format(int(time) // 100, int(time) % 100)
        return formatted_time
    
    def day_night_cycle(self):
            self.random_value = random.random()
            self.time = (self.time + self.time_increment) % 2400 

            if 800 <= self.time < 2000:
                opacity = 0
            else:
                if self.time < 800 or self.time >= 2400:  
                    opacity = self.max_opacity
                else:
                    if self.time < 800:  # sunrise
                        twilight_time = 800 - self.time
                    else:  # sunset
                        twilight_time = self.time - 2000
                    opacity = (twilight_time / 400) * self.max_opacity
                    opacity = min(opacity, self.max_opacity)

            self.night_opacity = opacity
            self.time_string = self.format_time(self.time)
    
    def reset_weather(self):
        self.current_weather = None
        self.current_sprite = 0
        self.weather_image = None

    def weather_cycle(self):
        if self.current_weather == None: # No weather
            if self.random_value < self.rain_frequency:
                self.current_weather = "rain"
        else:

            if random.random() < 0.001: # stop weather
                self.reset_weather()

            match self.current_weather:
                case "None":
                    pass
                case "rain":
                    self.current_sprite += self.rain_frame_speed
                    if self.current_sprite >= self.rain_frame_count:
                        self.current_sprite = 0
                    
                    self.weather_image = AssetManager.rain_sprites[int(self.current_sprite)]
