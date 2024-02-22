class Comment
{
    private object $author;
    protected string $text;
    protected string created_at
    protected string updated_at

    public function __construct(object $author, string $text)
    {
        $this->author = $author;
        $this->text = $text;
        $this->created_at = date("Y-m-d H:i:s");
        $this->updated_at = date("Y-m-d H:i:s");
    }

    public function getAuthor()
    {
        return $this->author;
    }

    public function getComment(string $text)
    {
        return $this->text;
    }

    public function setComment(string $text)
    {
        $this->text = $text;
        $this->updated_at = date("Y-m-d H:i:s");
    }
}
