# Documentation

## 6.4 Update Template URL Tags

When using Django's URL template tag, ensure it is properly formatted. For example:

```html
<a href="{{ '{% url my_view_name 'arg1'='value1' %}' }}">Link</a>
```

This way, Jekyll will not try to interpret the block as Liquid syntax, allowing it to remain functional within Django's context.

Make sure you test the URLs after updating to ensure everything is in working order.