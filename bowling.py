# -*- coding: utf-8 -*-


class MarkerError(Exception):
    pass


class BowlsLimit(Exception):
    pass


class FirstShot:

    def __init__(self, shot):
        self.shot = shot

    def result(self):
        point = 0
        if self.shot in ['/', '/']:
            raise MarkerError('Spare не может быть первым броском')
        elif self.shot in ['X', 'Х']:
            point += 10
            return point, True
        elif self.shot == '-':
            point += 0
            return point, SecondShot
        else:
            point += int(self.shot)
            return point, SecondShot


class SecondShot:

    def __init__(self, shot, check):
        self.shot = shot
        self.check = check

    def result(self):
        point = 0
        if self.shot in ['X', 'Х']:
            raise MarkerError('Знак "X" не может быть после первого броска')
        elif self.shot in ['/', '/']:
            point += 10
            return point, True
        elif self.shot == '-':
            point += 0
        else:
            point += int(self.shot)
            if self.check + point > 10:
                raise BowlsLimit('Сумма бросков больше 10')
        return point, FirstShot


class Games:

    def __init__(self, result):
        self.result = iter(str(result))
        self.just_res = result
        self.counter = -1
        self.score = 0
        self.check_score = 0

    def for_score(self, throw_number, numb):
        if throw_number == SecondShot:
            self.state = throw_number(shot=self.just_res[self.counter + numb], check=None)
        elif throw_number == FirstShot:
            self.state = throw_number(shot=self.just_res[self.counter + numb])
        new_score, new_state = self.state.result()
        self.score += new_score

    def strike_addition(self):
        self.score += 10
        self.state = True

    def spare_addition(self):
        self.score += 10
        self.state = True

    def state(self):
        while True:
            try:
                self.state = FirstShot(shot=next(self.result))
                self.counter += 1
            except StopIteration:
                break
            new_score, new_state = self.state.result()
            if new_state == True:
                self.score += new_score
                self.state = new_state
                self.strike_addition()
            else:
                self.score += new_score
                self.state = new_state
                try:
                    self.check_score = 0
                    self.check_score += new_score
                    self.state = SecondShot(shot=next(self.result), check=self.check_score)
                    new_score, new_state = self.state.result()
                    if self.state.shot not in ['/', '/']:
                        self.score += new_score
                        self.counter += 1
                    else:
                        self.score += new_score - self.check_score
                        self.state = new_state
                        self.spare_addition()
                except IndexError:
                    print('Индекс вне диапазона')
                except StopIteration:
                    break


class Native(Games):

    def strike_addition(self):
        self.score += 10

    def spare_addition(self):
        self.score += 5


class International(Games):

    def __init__(self, result):
        super().__init__(result)
        self.check_for_strike = []

    def strike_addition(self):
        self.check_for_strike.append(self.counter)
        try:
            if self.counter == 0 and self.just_res[self.counter + 2] not in ['/', '/'] or \
                    self.check_for_strike == [0, 1]:
                Games.for_score(self, FirstShot, 1)
                Games.for_score(self, FirstShot, 2)
            if self.check_for_strike[-1] - self.check_for_strike[-2] == 1 and self.check_for_strike != [0, 1]:
                Games.for_score(self, FirstShot, 1)
                if self.check_for_strike[-2] - self.check_for_strike[-3] == 1:
                    Games.for_score(self, FirstShot, 2)
        except IndexError:
            print('Индекс вне диапозона')

    def spare_addition(self):
        self.check_score = 0
        self.counter += 1
        if self.just_res[self.counter + 1] in ['X', 'Х']:
            self.score += 10
        else:
            self.state = SecondShot(shot=self.just_res[self.counter + 1], check=self.check_score)
            new_score, new_state = self.state.result()
            self.score += new_score
            try:
                if self.just_res[self.counter - 2] in ['X', 'Х']:
                    self.score += 10
            except IndexError:
                print('Индекс вне диапозона')


def game_score(score_rules, game_result):
    game_stat = score_rules(result=game_result)
    game_stat.state()
    return game_stat.score


def score_for_test(score_rules, game_result):
    try:
        return game_score(score_rules, game_result)
    except MarkerError as mark_exc:
        print(f'Исключение MarkerError {mark_exc}')
    except BowlsLimit as bl_exc:
        print(f'Исключение BowlsLimit {bl_exc}')
    except StopIteration:
        print('Конец итерации, результат: ', game_score(score_rules, game_result))
    except ValueError as val_exc:
        print(f'Исключение ValueError: {val_exc}')
    except Exception as exc:
        print(f'Поймано исключение {exc}')
