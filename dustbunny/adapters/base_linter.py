

class BaseLinter():
    ''''''

    def update(self):
        pass

    def retarget(self, new_target: str):
        self.target_path = new_target
        self.update()

    def report(self):
        if self.result is None:
            self.update()
        report_text = '\n'
        for field in self.result:
            report_text += (str(field) + '\n')
        return report_text
