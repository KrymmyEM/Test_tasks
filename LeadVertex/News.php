class News
{
    private $author;
    protected string $title;
    protected string $text;
    protected ?object $category;
    protected $comments;
    protected string created_at
    protected string updated_at

    public function __construct(object $author, string $title, string $text, ?object $category)
    {
        $this->author = $author;
        $this->title = $title;
        $this->text = $text;
        $this->category = $category;
        $this->comments = [];
        $this->created_at = date("Y-m-d H:i:s");
        $this->updated_at = date("Y-m-d H:i:s");
    }

    protected function setUpdateAt(){
        $this->updated_at = date("Y-m-d H:i:s");
    }

    public function getTitle()
    {
        return $this->title;
    }

    public function getText()
    {
        return $this->text;
    }

    public function getAuthor()
    {
        return $this->author;
    }

    public function getCategory()
    {
        return $this->category;
    }

    public function getComments()
    {
        return $this->comments;
    }

    public function getComment(int $index)
    {
        if (array_key_exists($index, $this->comments)) {
            return $this->comments[$index];
        }

        return FALSE
        
    }

    public function setTitle(string $title)
    {
        $this->title = $title;
        $this->setUpdateAt();
    }

    public function setText(string $text)
    {
        $this->text = $text;
        $this->setUpdateAt();
    }

    public function setCategory(object $category)
    {
        $this->category = $category;
        $this->setUpdateAt();
    }

    public function addComment(object $author, string $text)
    {
        $comment = new Comment($author, $text);
        $this->comments[] = $comment;
    }

    public function delCategory()
    {
        $this->category = NULL;
        $this->setUpdateAt();
    }

    public function delComment(int $index)
    {
        if (array_key_exists($index, $this->comments)) {
            unset($this->comments[$index])
            return TRUE
        }

        return FALSE
    }
}
