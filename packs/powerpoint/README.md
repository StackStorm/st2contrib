# PowerPoint 

This action enables the integration of StackStorm into Microsoft PowerPoint. This pack can be used to convert results of actions from other packs into a slide for convincing senior executives of important things.

## Configuration

The user can provide a corporate PowerPoint template by specifying a path in `config.yaml`

#### Make Presentation

Input :

```json
[
  {'layout' : 1 # The layout in the template - 1 based
   'title': 'my first slide'
   'text': 'The content of the slide!'}
]

```