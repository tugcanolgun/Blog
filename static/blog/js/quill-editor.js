_body = document.getElementById('id_body').value;
_editor = document.getElementById('editor');
_editor.innerHTML = _body;

var toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike',
        {
            'script': 'sub'
        }, {
            'script': 'super'
        },
    ],
    [{
        'color': []
        }, {
        'background': []
    }],
    [
        {
            'header': [false,3,2]
        },
    ],

    ['link', 'image', 'video'],
    ['blockquote', 'code-block', 
        {
            'list': 'ordered'
        }, {
            'list': 'bullet'
        }
        // ,{
        //     'list': 'check'
        // }
    ],
    [{
        'align': []
    }],
    ['clean']
];
var quill = new Quill('#editor', {
    theme: 'snow',
    placeholder: 'Write an article...',
    formula: true,
    syntax: true,
    modules: {
        toolbar: toolbarOptions
    }
});

quill.on('text-change', function (v) {
    var delta = quill.getContents();
    var qdc = new window.QuillDeltaToHtmlConverter(delta.ops, window.opts_ || {});
    var html = qdc.convert();
    var body = document.getElementById('id_body');
    // var htmlContent = quill.container.firstChild.innerHTML;
    body.value = html;
    // body.value = htmlContent;
    // console.log(htmlContent);
});
