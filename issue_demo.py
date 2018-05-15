'Test case, showing solution to dynamically constructed view problem.'
import numpy as np
from traits.api \
    import HasTraits, Str, Instance, Array, List
from traitsui.api \
    import View, Item, ModelView, InstanceEditor, ListEditor, Tabbed, VGroup, HGroup
from chaco.api \
    import ArrayPlotData, Plot
from enable.api \
    import ComponentEditor

    
class LineData(HasTraits):
    """ Data component of a measurement object, holds (x, y) data points.
    """
    x = Array
    y = Array

    def _x_default(self):
        return np.linspace(0.0, 5.0, 50.0)
    
    def _y_default(self):
        return self.x + np.random.uniform(-0.1, 0.1, self.x.shape[0])


class Measurement(HasTraits):
    """ A very simple measurement object just holding a line data model.
    """
    name = Str('Measurement')
    line_data = Instance(LineData)
    
    def _line_data_default(self):
        return LineData()

    
class MeasurementView(ModelView):
    """ A chaco (x, y) plot visualising measurement data.
    """
    model = Instance(Measurement)
    plot = Instance(Plot)
    data_source = Instance(ArrayPlotData)

    def _plot_default(self):
        plot = Plot(self.data_source, resizable='hv')  # resizable is ignored when in notebook?
        plot.plot(("x", "y"), type="line", color="blue")
        plot.title = "Title"
        return plot
 
    def _data_source_default(self):
        x = self.model.line_data.x
        y = self.model.line_data.y
        data_source = ArrayPlotData(x=x, y=y)
        return data_source
 
    def default_traits_view(self):
        name_item = Item('model.name')
        plot_item = Item('object.plot',
                         resizable=True,
                         show_label=False,
                         style = 'custom',
                         editor=ComponentEditor())
        group = HGroup(VGroup(name_item, plot_item, springy=True), springy=True)
        view = View(group,
                    resizable=True,
                    title="Measurement View",
                    )
        return view
 
class Robot(HasTraits):
    """ An robot which is measuring data.
    """
    measurement = Instance(Measurement)

    def _measurement_default(self):
        return Measurement()


class RobotView(ModelView):
    model = Instance(Robot)

    measurement_view = Instance(MeasurementView)
    
    def default_traits_view(self):
        view = View(
                    Item('object.measurement_view',
                         show_label=False,
                         style = 'custom',
                         editor=InstanceEditor(),
                         ),
                    resizable=True,
                    title="Robot View",
                    )
        return view
       
    def _measurement_view_default(self):
        return MeasurementView(self.model.measurement)


class Document(HasTraits):
    """ A document contains list of robot data sources which are measuring data.
    """
    robots = List(Robot)

    def _robots_default(self):
        return [Robot(), Robot()]


class DocumentView(ModelView):
    """ A document view displays multiple measurement views as notebook tabs.
    """
    model = Instance(Document)
    robot_views = List(RobotView)
    ui_title = Str('Document View')
 
    def _robot_views_default(self):
        return [RobotView(model=x) for x in self.model.robots]
 
    def default_traits_view(self):
        view = View(
                    Item('object.robot_views',
                         show_label=False,
                         style = 'custom',
                         editor=ListEditor(use_notebook=True, editor=InstanceEditor()),
                         ),
                    resizable=True,
                    title="{}".format(self.ui_title),
                    )
        return view

        
class MockApp(HasTraits):
    """ Mock applications root model object.
    """
    document = Instance(Document)

    def _document_default(self):
        return Document()

        
class MockAppView(ModelView):
    """ Mock applications root view object.
    """
    model = Instance(MockApp)
    document_view = Instance(DocumentView)
    doc_ui_title = Str('Document View')

    def default_traits_view(self):
        self.document_view.ui_title = self.doc_ui_title
        view = View(
                    Item('object.document_view',
                         show_label=False,
                         style = 'custom',
                         editor=InstanceEditor(),
                         ),
                    resizable=True,
                    title='App View',
                    )
        return view
    
    def _document_view_default(self):
        return DocumentView(model=self.model.document)


def test_app_view():
    model = MockApp()
    label = ('App View > Document View > Robot View (list) > Measurement View. '
             'Embedding Doc. View in App View causes broken layout.')
    view =  MockAppView(model=model, doc_ui_title=label)
    view.configure_traits()

def test_robot_view():
    model = Robot()
    view = RobotView(model=model)
    view.configure_traits()

def test_measurement_view():
    model = Measurement()
    view = MeasurementView(model=model)
    view.configure_traits()

def test_document_view():
    model = Document()
    label = ('Document View > Robot View (list) > Measurement View. '
             'Layout fine.')
    view = DocumentView(model=model, ui_title=label)
    view.configure_traits()

if (__name__ == '__main__'):
    test_document_view()
    test_app_view()
