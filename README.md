# traitsui-notebook-resize-bug
TraitsUI layout issue when for content of notebook view

Layout of the application is shown in the screenshot below.

It consists of Document View > (list of) Instrument Views > Measurement View

Note that the document view is using a `ListEditor(use_notebook=True)` so that
the insturments views all appear in their own tabs.

![Correct layout](https://raw.githubusercontent.com/danieljfarrell/traitsui-notebook-resize-bug/master/correct_layout.png)

Adding a new AppView view at the top of the hierarchy breaks the layout.

The new structure is App Vew > Document View > (list of) Instrument Views > Measurement View

![Borken layout](https://raw.githubusercontent.com/danieljfarrell/traitsui-notebook-resize-bug/master/layout_issue.png)

